<?php
/*
 * Set config
 */
define('REPLY_URL','https://m.api.weibo.com/2/messages/reply.json');
# 和守护进程通信的key,一致即可，长度不限
define('ACCESS_TOKEN','xxxxxxxxxxxx');
# APP_KEY这个应用所有者（注意应用所有者可以不是需要获取消息的认证用户，认证用户指定该应用开发就行）的微博登录名
define('USERNAME','xxx@xxx.com');
# APP_KEY这个应用所有者的微博登录密码
define('PASSWORD','password');
# 指定用于开发模式的应用appkey，详见：http://t.cn/zRp0sr6
define('SOURCE_ID','');
# 认证用户的微博ID，认证用户需已指定APP_KEY开发。如何指定：http://t.cn/zRp0sr6
define('WEIBO_UID','');
