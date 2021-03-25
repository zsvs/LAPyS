<?php
require_once ("classes/DBCreate.php");
require_once ("classes/FillTable.php");
require_once ("classes/ValueTable.php");

$get = new ValueTable('svs');
$set = new FillTable('svs');

$set->insert();
$get->getTableValue();
