<?php
require 'var_conn.php';

session_start();

if ($_SESSION["autenticado"] == 1) {
    header("Location: " . $_SESSION['usuario']);
    exit();
}

if (isset($_POST['login']) and isset($_POST['senha']))
{
	$login=$_POST['login'];
	$senha=$_POST['senha'];
}
else {
	die('Erro na passagem de parametros');
}

$result = $bd->query("SELECT * from projeto_users where email='$login' and senha='$senha'");

if ($line = $result->fetch_assoc()) {
    $_SESSION["autenticado"] = 1;
    $_SESSION['user'] = $line['email'];
    $_SESSION['usuario'] = $line['tipo'];
    $_SESSION['userid'] = $line['uid'];
    $_SESSION['login'] = $line['primeiro_acesso'];
    header("Location: " . $_SESSION['usuario']);
    exit();
} else {
    $_SESSION["autenticado"] = 0;
    header("Location: index.php");
    exit();
}
?>
