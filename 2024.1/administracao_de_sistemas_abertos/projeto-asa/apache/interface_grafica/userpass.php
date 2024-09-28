<?php
require 'var_conn.php';

session_start();

if (isset($_GET['id']))
{
	$userid = $_GET['id'];
	$pass = bin2hex(openssl_random_pseudo_bytes(8));
	$hash = "{SHA}" . base64_encode(sha1($pass, TRUE));
}
else {
	die('Erro na passagem de parametros');
}  	

$bd->query("UPDATE projeto_users SET senha='$pass', primeiro_acesso='1', senha_apache='$hash' WHERE uid=" . $userid);
header('Refresh: 5; URL=admdom.php');
echo "Senha do usuario: " . $pass;
?> 
