<?php
    $dsn = 'mysql:host=localhost;dbname=jordantechsupport';
    $username = 'jsteurer5';
    $password = '276831';

    try {
        $db = new PDO($dsn, $username, $password);
    } catch (PDOException $e) {
        $error_message = $e->getMessage();
        include('../errors/database_error.php');
        exit();
    }
?>