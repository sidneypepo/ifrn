<?php
require 'var_conn.php';

session_start();

if (isset($_POST['novodom'])) {
        if (empty($_POST["novodom"])) {
                header('Refresh: 4; URL=admgeral.php');
                echo "Dominio invalido, tente novamente";
                exit();
        } else {
                $dominio = $_POST['novodom'];
                $pass = bin2hex(openssl_random_pseudo_bytes(8));
                $hash = "{SHA}" . base64_encode(sha1($pass, TRUE));
                $adm = "root@" . $dominio;
                $name = "root_" . $dominio;
        }
} else {
        die('Erro na passagem de parametros');
}
  
$result = $bd->query("SELECT COUNT(*) AS count FROM domains WHERE domain = '$dominio'");
if ($result) {
    $row = $result->fetch_assoc();
    $count = $row['count'];
    $result->close();
}

if ($count > 0) 
{
	header('Refresh: 5; URL=admgeral.php');
        echo "Dominio ja existe, tente novamente";
	exit();
}

$bd->query("INSERT INTO domains (domain) VALUES ('{$dominio}')");
$bd->query("INSERT INTO projeto_users (nome,login,email,senha,ativo,tipo,dominio,primeiro_acesso,senha_apache) VALUES ('{$name}', '{$name}', '{$adm}', '{$pass}', 's', 'admdom.php', '{$dominio}', '1', '{$hash}')");

//exec("/var/projeto-asa/apache/scripts/atualizar_apache.py", $output, $return_var);
//if ($return_var !== 0) {
//	echo "Erro ao executar atualizar_apache.py: " . implode("\n", $output);
//	exit();
//}

//exec("/bin/bash /var/projeto-asa/dns/scripts/adicionando_dominio.sh", $output, $return_var);
//if ($return_var !== 0) {
//        echo "Erro ao executar adicionando_dominio.sh: " . implode("\n", $output);
//        exit();
//   }

shell_exec("/var/projeto-asa/apache/scripts/exeroot & disown");

header('Refresh: 10; URL=admgeral.php');
echo "Senha do administrador: " . $pass;
?>
