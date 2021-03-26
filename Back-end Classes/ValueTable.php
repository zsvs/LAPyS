<?php


class ValueTable extends DBCreate
{
    public function __construct(string $database = "")
    {
        parent::__construct($database);
    }
    public function __destruct()
    {
        parent::__destruct();
    }

    public function getTableValue(){
        $request = $this->mysqli->query("select login, password, inet_ntoa(IP_Address) as ip_address, data_create from data;");
        foreach ($request->fetch_assoc() as $key=>$value){
            echo "$key => $value" . "<br>";
        }
    }
}
