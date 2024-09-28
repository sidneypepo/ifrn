<?php
require 'var_conn.php';

session_start();

if (isset($_POST['novousr'])) {
        if (empty($_POST["novousr"])) {
                header('Refresh: 4; URL=' . $_SESSION['usuario']);
                echo "Nome invalido, tente novamente";
                exit();
        } else {
                $usr = $_POST['novousr'];
                $pass = bin2hex(openssl_random_pseudo_bytes(8));
                $hash = "{SHA}" . base64_encode(sha1($pass, TRUE));
                $search = "@";
                $pos = strpos($_SESSION['user'], $search);
                $dominio = substr($_SESSION['user'], $pos);
                $dom = substr($_SESSION['user'], $pos+strlen($search));
                $newusr = $usr . $dominio;
        }
} else {
        die('Erro na passagem de parametros');
}

$result = $bd->query("SELECT COUNT(*) AS count FROM projeto_users WHERE email = '$newusr'");

if ($result) {
    $row = $result->fetch_assoc();
    $count = $row['count'];
    $result->close();
} 

if ($count > 0) {
        echo "usuario ja existe";
        header('Refresh: 4; URL=admdom.php');
        exit();
}

$bd->query("INSERT INTO projeto_users (nome,login,email,senha,ativo,tipo,dominio,primeiro_acesso,senha_apache) VALUES ('{$usr}', '{$usr}', '{$newusr}', '{$pass}', 's', 'comum.php', '{$dom}', '1', '{$hash}')");
header('Refresh: 10; URL=admdom.php');
echo "Senha do usuario: " . $pass;

//shell_exec("/var/projeto-asa/ftp/ftpconfig.sh");
shell_exec("/var/projeto-asa/apache/scripts/exeroot");
?>
