<?php

class FillTable extends DBCreate
{
    public function __construct(string $database = "")
    {
        parent::__construct($database);
    }

    public function __destruct()
    {
        parent::__destruct();
    }

    public function insert()
    {
        $this->mysqli->query("INSERT INTO `data` (`id`, `login`, `password`, `IP_Address`, `data_create`, `data_update`) VALUES (NULL, 'bogdan', (1,AES_ENCRYPT('user', UNHEX(SHA2('svsthebest', 52)))), inet_aton('192.168.0.1'), '2021-03-24 05:21:00', CURRENT_TIMESTAMP)");
    }
}
