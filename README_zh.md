# CVE-2022-47745

English : [README.md](./README.md)

ZenTao是中国研发团队的头号团队协作工具，拥有140万用户。它有许多用户，如Twitter、联想等。以下是它的官方网站：https://www.zentao.pm/（英语）和https://www.zentao.net/（中文）。

控制器convert的importNotice方法存在sql注入漏洞，通过发送特殊构造的请求报文，即可完成sql注入。由于这里的sql注入为堆叠注入，可以执行任意sql语句，因此在配置不当的情况下可以直接通过sql语句getshell。

通过访问misc-captcha-user.html，我们可以获取到一个合法的zentaosid（cookie），因此可以直接在前台完成sql注入。

# 影响版本

16.4 <= versions <= 18.0.beta1

该漏洞目前已经被修复，您可以参考这个issue：https://github.com/easysoft/zentaopms/issues/106

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
