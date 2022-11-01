#!/usr/bin/php
<?php

define("PATH_DOCKER_COMPOSE_YML", "/code/ux_drop_box_undetected_chrome/docker-compose.yml");

function executeDockerDropBoxUx()
{
    // levantando contenedor docker
    $commandUpContainer = "docker compose -f " . constant('PATH_DOCKER_COMPOSE_YML') . " up -d 2>&1";
    $commandExecUxDropBox = "docker compose exec selenium /env/bin/python3 /app/inicio_ux_dropbox.py";
    $commandStopContainer = "docker compose -f " . constant('PATH_DOCKER_COMPOSE_YML') . " stop 2>&1";
    $commandDeleteContainer = "docker compose -f " . constant('PATH_DOCKER_COMPOSE_YML') . " rm -fsv 2>&1";
    $json_result = '';
    $result = '';

    // deteniendo el container
    $result = shell_exec($commandStopContainer);

    // iniciando el container
    $result = shell_exec($commandUpContainer);

    // espera unos 10 segundos despues de levantar el container
    sleep(10);

    // ejecutando comando de ux
    $result = shell_exec($commandExecUxDropBox);

    foreach (preg_split("/((\r?\n)|(\r\n?))/", $result) as $line) {
        if (strpos($line, "Xlib.xauth: warning") === false) {
            $json_result = $json_result . $line;
        }
    }

    // eliminando el contenedor
    $result = shell_exec($commandDeleteContainer);
    printf($result);
    $json_result = json_decode($json_result);

    return $json_result;
}

$result = executeDockerDropBoxUx();
print_r($result);
