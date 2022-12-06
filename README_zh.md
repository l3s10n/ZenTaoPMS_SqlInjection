# 概述

English : [README.md](./README.md)

使用任意用户登录之后，通过向控制器convert的importNotice方法发送特殊构造的请求报文，即可完成sql注入。

# 原理

这里是importNotice方法的部分源码:

```php
public function importNotice($method = 'db')
{
    if($this->server->request_method == 'POST')
    {
        if($method == 'db')
        {
            $dbName = $this->post->dbName;
            if(!$dbName)
            {
                $response['result']  = 'fail';
                $response['message'] = $this->lang->convert->jira->dbNameEmpty;
                return print($this->send($response));
            }

            if(!$this->convert->dbExists($dbName))
            {
                ...

}
```

我们可以通过url `/index.php?m=convert&f=importNotice&zentaosid=xxx`来访问到上述代码，这里的`zentaosid`是cookie的一部分，可以来自于任意已登录的用户。`$this->post->dbName`来自post报文的数据段，这意味着$dbName是可控的。

这里是`dbExists`的源码：

```php
public function dbExists($dbName = '')
{
    $sql = "SHOW DATABASES like '{$dbName}'";
    return $this->dbh->query($sql)->fetch();
}
```

我们可以通过设置$dbName为`'; <sql_statement> #`完成sql语句的执行。

# 演示

详见本仓库的Demonstrate.mp4文件

# exp

详见本仓库的exp.py文件

# 免责声明

本仓库仅用于学习，请勿用于实际场景，一切后果由使用者自负。
