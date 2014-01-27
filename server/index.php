<?php
define('BASE', dirname(__FILE__));
require( BASE.'/config.php');
$access_token = $_POST['token'];
if ($access_token != ACCESS_TOKEN ) {
    die('Permission check failed!');  
}
$data = $_POST['data'];
$data = json_decode($data, true);
$message_id = $data['id'];
$type_in = $data['type'];
$sender_id = $data['sender_id'];
$text = $data['text'];
$type = "articles";
$replayText = json_encode(
    array(
        "articles" => array(
            array(
                'display_name' => '消息服务 - "' . $text . '"',
                'summary' => '消息服务是为认证帐号、应用提供的与微博用户进行消息互动的服务。<200b>',
                'image' => 'http://storage.mcp.weibo.cn/0JlIv.jpg',
                'url' => 'http://open.weibo.com/wiki/Messages'
            )   
        )   
    )   
);
$post = array(
    "id" => $message_id,
    'source' => SOURCE_ID,
    "type" => $type,
    "data" => $replayText,
);
$ret = httpPost($post, REPLY_URL, USERNAME, PASSWORD);
echo $ret;

function httpPost($args, $url, $user, $passwd, $timeout = 30) 
{                     
    $postdata = http_build_query($args);                                                          
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);                                                          
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
    curl_setopt($ch, CURLOPT_USERPWD, $user . ':' . $passwd);                                     
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);                                                  
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);                                              
    $data = curl_exec($ch);                                                                       
    curl_close($ch);                                                                              
    return $data;                                                                                 
}
