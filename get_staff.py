#!/usr/bin/python

import requests
import os
import shutil
import json
import datetime
import config
import logging


def get_staff_token(url, password, from_action_version, from_details_version):
    req = {
        "versionActionsFrom": from_action_version,
        "versionDetailsFrom": from_details_version,
        "versionActionsTo": 9999999,
        "versionDetailsTo": 9999999,
        "password": password
    }
    log.info("Getting staff token")
    log.info("  from_actions_version: {}".format(from_action_version))
    log.info("  from_details_version: {}".format(from_details_version))
    response = requests.post(url, json=req)
    return response.json()['token']


def get_image_token(url, password):
    log.info("Getting image token")
    req = {
        'password': password
    }
    response = requests.post(url, json=req)
    return response.json()['token']


def get_staff_data(request_token):
    url = config.STAFF_DATA_URL.format(request_token)
    log.info("Getting: {}".format(url))
    response = requests.get(url)
    with open("staff_data.json", 'w') as output:
        json.dump(json.loads(clean_downloaded_text(response.text)), output)
    return json.loads(clean_downloaded_text(response.text))


def clean_downloaded_text(input_data):
    return input_data.replace("\\u200b", "").replace("\u200b", "").replace(u'\xa0', u' ')


def get_staff_image(request_token, staff_id, filetype):
    url = config.STAFF_IMAGE_URL.format(request_token, staff_id, filetype)
    log.info("Getting: {}".format(url))
    output_file_path = os.path.join(config.OUTPUT_IMAGE_DIRECTORY, str(staff_id) + "." + filetype)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file_path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    else:
        log.error("Error {} getting file {}".format(response.status_code, url))


def get_replacement_department_name(department):
    lowercase_department = department.lower()
    if lowercase_department in config.REPLACE_DEPARTMENTS:
        return config.REPLACE_DEPARTMENTS[lowercase_department]
    else:
        return department


def get_replacement_position_name(position):
    pos = position.lower()
    if pos in config.REPLACE_POSITIONS:
        return config.REPLACE_POSITIONS[pos]
    else:
        return position.replace("Assistant", 'Asst.')


def load_run_info(filename):
    try:
        log.info("Loading last run information from " + filename)
        with open(filename, "r") as in_file:
            return json.load(in_file)
    except IOError:
        log.warning("Error reading staff.json, using defaults")
        return {"last_run_time": datetime.datetime.now().isoformat(),
                "last_actions_version": 0,
                "last_details_version": 0
                }


def save_last_run_info(filename, configuration_dict):
    try:
        log.info("Saving updated configuration file " + filename)
        json_config = json.dumps(configuration_dict, indent=True)
        with open(filename, 'w') as out_file:
            out_file.write(json_config)
    except IOError as ex:
        log.error("Error saving config file staff.json", ex)
    except TypeError as ex:
        log.error("Error serializing configuration to JSON. Run information not saved.", ex)


def update_last_run(configuration, downloaded_data):
    if 'detailsVersion' in downloaded_data:
        if configuration['last_details_version'] != downloaded_data['detailsVersion']:
            log.info("updating detailsVersion {} -> {}".format(configuration['last_details_version'], downloaded_data['detailsVersion']))
            configuration['last_details_version'] = downloaded_data['detailsVersion']
    if 'actionsVersion' in downloaded_data:
        if configuration['last_actions_version'] != downloaded_data['actionsVersion']:
            log.info("updating actionsVersion {} -> {}".format(configuration['last_actions_version'], downloaded_data['actionsVersion']))
            configuration['last_actions_version'] = downloaded_data['actionsVersion']
    configuration['last_run_time'] = datetime.datetime.now().isoformat()


def download_images(image_token, downloaded_data):
    if 'persons' in downloaded_data and len(downloaded_data['persons']) > 0:
        log.info("Downloading images...")
        image_count = 0
        person_count = 0
        for person in downloaded_data['persons']:
            person_count += 1
            if "badgeImageFileType" in person and person['badgeImageFileType'] != '':
                image_count += 1
                log.debug("Downloading image for: %s", person['namePrivacy'])
                get_staff_image(image_token, person['id'], person['badgeImageFileType'])

        log.info("Downloaded %s images for %s people", image_count, person_count)


def process_actions(input_data):
    if 'deleted' in input_data and len(input_data['deleted']) > 0:
        log.info("Found deleted actions version %s: %s", input_data['actionsVersion'], input_data['deleted'])
        output_path = os.path.join(config.OUTPUT_JSON_DIRECTORY, 'deleted.json')
        with open(output_path, 'w') as output_file:
            output_file.write(json.dumps({
                'actions': [{
                    'actionsVersion': input_data['actionsVersion'],
                    'deleted': input_data['deleted']}]}))


def process_persons(input_data):
    if 'persons' in input_data:
        log.info("Found %s persons in version %s", len(input_data['persons']), input_data['detailsVersion'])
        for person in input_data['persons']:
            if 'tShirtSize' in person:
                shirt = person['tShirtSize']
                if shirt.strip() == '':
                    shirt = 'not provided'
                person['notes'] = []

                person['notes'].append("T-Shirt size: " + shirt)
            for i in range(len(person['positions'])):
                dept = person['positions'][i]['department']
                title = person['positions'][i]['title']
                person['positions'][i]['department'] = get_replacement_department_name(dept)
                person['positions'][i]['title'] = get_replacement_position_name(title)

            path = os.path.join(config.OUTPUT_JSON_DIRECTORY, str(person['id']) + '.json')
            with open(path, 'w') as out_file:
                out_file.write(json.dumps({
                    'persons': [person],
                    'detailsVersion': input_data['detailsVersion']
                }))

def create_directory(dir_path):
    try:
        os.mkdir(dir_path)
        log.info("Created {}".format(dir_path))
    except FileExistsError:
        log.info("Output directory {} exists".format(dir_path))


if __name__ == '__main__':
    logging.basicConfig(filename=config.LOG_FILENAME, level=config.LOG_LEVEL, format='%(asctime)s - %(message)s')
    log = logging.getLogger('get_staff')
    ch = logging.StreamHandler()
    log.addHandler(ch)
    log.info("Starting up...")

    create_directory(config.OUTPUT_IMAGE_DIRECTORY)
    create_directory(config.OUTPUT_JSON_DIRECTORY)

    last_run = load_run_info(config.LAST_RUN_FILENAME)

    token = get_staff_token(config.STAFF_TOKEN_URL, config.PASSWORD, last_run['last_actions_version'], last_run['last_details_version'])
    log.debug("Got token: {}".format(token))
    data = get_staff_data(token)

    process_actions(data)
    process_persons(data)
    update_last_run(last_run, data)
    image_token = get_image_token(config.IMAGE_TOKEN_URL, config.PASSWORD)
    download_images(image_token, data)

    save_last_run_info(config.LAST_RUN_FILENAME, last_run)
