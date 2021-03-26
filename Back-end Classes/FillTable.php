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

    public string $ip;

    protected array $test = array("username" => 'Иван',
                                  "password" => 'Иванов',
                                  "RequestedName" => "ENS-SHYLO-NB");
    public function insert()
    {
        /*$json = '{"UserID": {"UserName": "sa.stepanets", "Password": "$SOME_UGLY_BASTARD_PASSWORD$", "RequestedName": "SOME_NAME", "Date": "2021-03-24 20:12:55.103612"}}';
        $array = json_decode($json, true);
        */

        $this->mysqli->query("INSERT INTO `data` (`id`, `login`, `password`, `RequestedName`, `IP_Address`, `data_create`, `data_update`) VALUES (NULL, 'oleg', '12asfa2', 'ENS-SHYLO-NB', inet_aton('$this->ip'), '2021-03-24 05:21:00', CURRENT_TIMESTAMP)");
    }
}
