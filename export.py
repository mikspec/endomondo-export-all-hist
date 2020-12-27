import argparse
import json
import logging
import os
import requests

_HOST = "www.endomondo.com"
_LIMIT = 15


def login(args, request):
    logging.debug(f'user {args.user}, pass {args.password}')
    request.headers['User-Agent'] = 'PostmanRuntime/7.26.8'
    request.headers['Content-Type'] = 'application/json'

    payload = {"email": args.user,
               "password": args.password, "remember": True}

    login_resp = request.post(
        'https://'+_HOST+'/rest/session', data=json.dumps(payload))

    return login_resp


def get_gpx(request, login_resp, user, workout):
    workout_url = f'https://{_HOST}/rest/v1/users/{user}/workouts/{workout["id"]}/export?format=GPX'
    gpx = request.get(workout_url, cookies=login_resp.cookies)
    logging.info(workout_url)
    file2 = open(f'{workout["id"]}.gpx', 'w+')
    file2.write(gpx.text)
    file2.close()    

def history(request, login_resp, endo):
    continue_flag = True
    hist_next = f'/rest/v1/users/{endo["user"]["id"]}/workouts/history?offset=0&limit={_LIMIT}&expand=workout:full'
    while continue_flag:
        hist_resp = request.get(
            f'https://{_HOST}{hist_next}', cookies=login_resp.cookies).json()
        logging.info(hist_resp["paging"]["next"])
        for i in hist_resp["data"]:
            endo["data"].append(i)
            try:
                get_gpx(request, login_resp, endo["user"]["id"], i)
            except Exception as e:
                logging.error(f'Unexpected Error: {e}')

        continue_flag = (hist_resp["paging"]["total"] > len(endo["data"]))
        hist_next = hist_resp["paging"]["next"]


def write_json(endo):
    file1 = open(f'{endo["user"]["id"]}.json', 'w+')
    file1.write(json.dumps(endo))
    file1.close()


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Endomondo data export')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='Increase verbosity (logs all data going through)')
    parser.add_argument('-u', dest='user',
                        help='Endomondo user')
    parser.add_argument('-p', dest='password',
                        help='Endomondo password')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s.%(msecs)d | %(levelname)s | %(filename)s: %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if args.verbose else logging.INFO)

    logging.info("Export start")
    request = requests.session()
    login_resp = login(args, request)

    endo = {"user": login_resp.json(), "data": []}
    history(request, login_resp, endo)
    logging.info("Export end")

    write_json(endo)


if __name__ == "__main__":
    main()
