from app import UPLOAD_FOLDER
import os, requests
from app.db_connection import get_db


def save_image(request, key):
    img_url = request.form.get('img_url')
    if img_url == "":
        file = request.files['img_file']
        _, extension = os.path.splitext(file.filename)
        filename = key + extension
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        jsonReq = {"key":key}
        res = requests.post('http://localhost:5001/invalidate', json=jsonReq)
        return write_img_db(key, filename)
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            _, extension = os.path.splitext(img_url)
            filename = key + extension
            with open(UPLOAD_FOLDER + "/" + filename, 'wb') as f:
                f.write(response.content)
            jsonReq = {"key":key}
            res = requests.post('http://localhost:5001/invalidate', json=jsonReq)
            return write_img_db(key, filename)
        return "INVALID"
    except:
        return "INVALID"

def write_img_db(image_key, image_tag):

    if image_key == "" or image_tag == "":
        error_msg="FAILURE"
        return error_msg
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query_exists = "SELECT EXISTS(SELECT 1 FROM image_table WHERE image_key = (%s))"
        cursor.execute(query_exists,(image_key,))
        for elem in cursor:
            if elem[0] == 1:
                query_remove = '''DELETE FROM image_table WHERE image_key=%s'''
                cursor.execute(query_remove,(image_key,))
                break

        query_add = ''' INSERT INTO image_table (image_key,image_tag) VALUES (%s,%s)'''
        cursor.execute(query_add,(image_key,image_tag))
        cnx.commit()

        return "OK"
    except:
        return "FAILURE"
