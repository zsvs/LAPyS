<?php

class DBCreate
{
    /**
     * @var string
     * The hostname localhost has a special meaning. It is bound to the use of Unix domain sockets.
     * To open a TCP/IP connection to the localhost, 127.0.0.1 must be used instead of the hostname localhost.
     */
    protected string $host = "localhost";
    /**
     * @var string
     */

    protected string $user = "root";
    /**
     * @var string
     */
    protected string $password = "root";

    /**
     * @var string
     */
    protected string $database;

    /**
     * @var mysqli|object
     */
    protected object $mysqli;

    /**
     * @var object
     */
    protected object $result;


    public function __construct(string $database = "")
    {
        $this->mysqli = new mysqli($this->host, $this->user, $this->password, $this->database = $database);
        if ($this->mysqli->connect_errno) {
            die('Ошибка соединения: ' . $this->mysqli->connect_errno);
        }
    }

    public function __destruct()
    {
        $this->mysqli->close();
    }

    public function createDataBase(string $nameDataBase)
    {
        $this->result = $this->mysqli->query("SHOW DATABASES LIKE '$nameDataBase'");
        if ($this->result->{'num_rows'} == 0) {
            $this->mysqli->query("CREATE DATABASE $nameDataBase");
            echo "DataBase '$nameDataBase' successful created!";
        } else if ($this->result->{'num_rows'} >= 1) {
            echo "DataBase '$nameDataBase' already exist!";
        } else {
            echo "Nothing happened";
        }
    }

    public function createTable()
    {
        $this->result = $this->mysqli->query("SHOW TABLES LIKE 'data'");
        if ($this->result->{'num_rows'} == 0) {
            $this->mysqli->query("CREATE TABLE `svs`.`data` (
            `id` INT NOT NULL AUTO_INCREMENT ,
            `login` VARCHAR(50) NOT NULL ,
            `password` VARCHAR(600) NOT NULL ,
            `IP_Address` int UNSIGNED NOT NULL ,
            `data_create` TIMESTAMP NOT NULL ,
            `data_update` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE = InnoDB DEFAULT CHARSET=utf8;");
            echo "Таблица успешно создана!";
        } else {
            echo "Такая таблица уже создана!";
        }
    }
}
