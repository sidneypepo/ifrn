<?php
$host = "192.168.102.100";
$usuario = "container20";
$senha = "1F(986934)";
$banco = "BD20";

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

try {
    $bd = new mysqli($host, $usuario, $senha, $banco);
} catch (mysqli_sql_exception $e) {
    echo "Error: " . $e->getMessage();
}
?>

