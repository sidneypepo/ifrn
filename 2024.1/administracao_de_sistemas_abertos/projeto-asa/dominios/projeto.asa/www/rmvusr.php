<?php
require 'var_conn.php';

if (isset($_GET['id']))
{
	$usr = $_GET['id'];
	
}
else
	die('Erro na passagem de par&acirc;metros');
  
$bd->query("DELETE FROM projeto_users WHERE uid =" . $usr);
header("Location: admdom.php");
shell_exec("/var/projeto-asa/apache/scripts/exeroot & disown");
?> 

