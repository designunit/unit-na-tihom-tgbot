import sys
import gridfs
import argparse


from mongo_ops import connect


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', required=True, help='file location')
    parser.add_argument('-l', '--label', required=True, help='file label')

    args = parser.parse_args()

    conn = connect()

    db = conn["tixiy_bot_db"]
    fs = gridfs.GridFS(db)

    name = args.file
    name_label = args.label

    file_location = f"/mnt/c/Users/modernpacifist/Documents/github-repositories/unit-na-tihom-tgbot/separate_events_jpg/{name}"

    try:
        with open(file_location, "rb") as file:
            data = file.read()

        fs.put(data, label=name_label, filename=file.name)
        print("upload completed")

    except Exception as e:
        print(e)
        exit(1)