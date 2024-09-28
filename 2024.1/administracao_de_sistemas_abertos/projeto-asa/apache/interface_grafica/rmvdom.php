<?php
require 'var_conn.php';

if (isset($_GET['dom']))
{
	$dominio = $_GET['dom'];
}
else
	die('Erro na passagem de parametros');
  
$bd->query("DELETE FROM domains WHERE domain='$dominio'");
$bd->query("DELETE FROM projeto_users WHERE dominio='$dominio' AND (tipo='comum.php' OR tipo='admdom.php')");

//exec("/usr/bin/python3 /var/projeto-asa/apache/scripts/atualizar_apache.py", $output, $return_var);
//if ($return_var !== 0) {
//        echo "Erro ao executar atualizar_apache.py: " . implode("\n", $output);
//        exit();
//}

//exec("/bin/bash /var/projeto-asa/dns/scripts/apagando_dominio.sh", $output, $return_var);
//if ($return_var !== 0) {
//        echo "Erro ao executar apagando_dominio.sh: " . implode("\n", $output);
//        exit();
//   }

shell_exec("/var/projeto-asa/apache/scripts/exeroot");

header("Location: admgeral.php");
?> 

