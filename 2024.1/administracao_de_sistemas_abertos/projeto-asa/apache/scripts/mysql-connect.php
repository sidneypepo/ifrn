#!/usr/bin/php
<?php
// Preencha com os dados do seu container
$host = "192.168.102.100";
$user = "container20";
$senha ="1F(986934)";
$bd = "BD20";

$conectar = new mysqli($host, $user, $senha, $bd);

$sql = "SELECT domain FROM domains";

$result = $conectar->query($sql);

if ($result->num_rows > 0) {
    echo "domain\n";
    while ($row = $result->fetch_assoc()) {
        echo $row["domain"] . "\n";
    }
} 

$conectar->close();
?>
