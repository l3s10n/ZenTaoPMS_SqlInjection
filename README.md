# Abstract

中文 : [README_zh.md](./README_zh.md)

After logging in with any user, you can complete SQL injection by constructing a special request and sending it to function importNotice of controller convert.

# Principle

Here is a section of source code of the function importNotice:

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

We can use url `/index.php?m=convert&f=importNotice&zentaosid=xxx` to access this function, and `zentaosid` is part of the cookie of any logged-in user. Besides, `$this->post->dbName` is from data segment of our post request, which means we can control the value of $dbName.

And here is the source code of `dbExists`：

```php
public function dbExists($dbName = '')
{
    $sql = "SHOW DATABASES like '{$dbName}'";
    return $this->dbh->query($sql)->fetch();
}
```

Since we can control the value of dbName, we can set its value to `'; <sql_statement> #`.

# Demonstrate

you can see it at Demonstrate.mp4 of this repository

# exp

you can get it at exp.py of this repository