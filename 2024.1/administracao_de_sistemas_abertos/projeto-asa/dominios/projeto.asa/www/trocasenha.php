<?php
require 'var_conn.php';

session_start();

if (isset($_POST['novasenha'])) {
	if (empty($_POST["novasenha"])) {
		header('Refresh: 4; URL=' . $_SESSION['usuario']);
		echo "Senha invalida, tente novamente";
		exit(); 
	} else {
		$pass = $_POST['novasenha'];
                $hash = "{SHA}" . base64_encode(sha1($pass, TRUE));
	}
} else {
	die('Erro na passagem de parametros');
}  

$bd->query("UPDATE projeto_users SET senha='$pass', senha_apache='$hash' WHERE uid=" . $_SESSION['userid']);

if ($_SESSION["login"] == 0) {
    
    header("Location: " . $_SESSION['usuario']);
} 
else {
    $bd->query("UPDATE projeto_users SET primeiro_acesso=0 WHERE uid=" . $_SESSION['userid']);
    header("Location: sair.php");
}
?> 
