
===================

用于新浪微博粉丝服务。

部署说明
--------

+ 修改config.ini文件中的配置信息
+ 修改server/config.php中的配置信息
+ 找一台能访问公网的机器起一个守护进程，参考如下守护进程
+ 将server下的代码部署到web服务器，参考如下web端


守护进程
--------

其中``lazyfans.py``为守护进程脚本，需要找一台可以访问公网的机器部署。守护进程的作用为长连接新浪微博推消息接口，一旦有新的私信，将其转发到web端处理。

部署脚本：

```
#nohup lazyfans.py &
```

web端
--------

web端是一个php脚本，你也可以使用其他的语言改写，作用是接受守护进程推送过来的消息，并按照你的处理逻辑得到响应的结果，然后将其发送给发私信的用户，完成一次交互。

Bug tracker
-----------

Have a bug? Please create an issue here on GitHub!

https://github.com/xiaosier/lazyfans/issues


Author
-------

+ http://weibo.com/lazypeople
+ http://lazy.changes.com.cn



