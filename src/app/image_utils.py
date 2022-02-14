from app import UPLOAD_FOLDER
import os, requests
from db_connection import get_db


def save_image(request, key):
    img_url = request.form.get('img_url')
    if img_url == "":
        file = request.files['img_file']
        _, extension = os.path.splitext(file.filename)
        filename = key + extension
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        jsonReq = {key:filename}
        res = requests.post('http://localhost:5001/put', json=jsonReq)
        return str(res.json())
    
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            _, extension = os.path.splitext(img_url)
            filename = key + extension
            with open(UPLOAD_FOLDER + "/" + filename, 'wb') as f:
                f.write(response.content)
            jsonReq = {key:filename}
            res = requests.post('http://localhost:5001/put', json=jsonReq)
            return str(res.json())
        return "INVALID"
    except:
        return "INVALID"

def write_img_db(image_key, image_tag):

    if image_key == "" or image_tag == "":
        error_msg="Error: All fields are required!"
    


    cnx = get_db()
    cursor = cnx.cursor()
    query_exists = "SELECT EXISTS(SELECT 1 FROM image_table WHERE image_key = %s)"
    cursor.execute(query_exists,(image_key))
    print(cursor)
    # query = ''' INSERT INTO image_table (image_key,image_tag)
    #                    VALUES (%s,%s)
    # '''

    # cursor.execute(query,(image_key,image_tag))
    # cnx.commit()

    return True
