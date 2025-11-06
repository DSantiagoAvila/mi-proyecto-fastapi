-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-11-2025 a las 03:31:20
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `resultados`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `procesos`
--

CREATE TABLE `procesos` (
  `ID` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  `category` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `procesos`
--

INSERT INTO `procesos` (`ID`, `value`, `category`) VALUES
(901, 93, 'good'),
(902, 87, 'good'),
(903, 65, 'medium'),
(904, 99, 'good'),
(905, 71, 'medium'),
(906, 71, 'medium'),
(907, 92, 'good'),
(908, 93, 'good'),
(909, 88, 'good'),
(910, 89, 'good'),
(911, 80, 'medium'),
(912, 77, 'medium'),
(913, 64, 'medium'),
(914, 87, 'good'),
(915, 98, 'good'),
(916, 74, 'medium'),
(917, 70, 'medium'),
(918, 87, 'good'),
(919, 92, 'good'),
(920, 87, 'good'),
(921, 93, 'good'),
(922, 74, 'medium'),
(923, 81, 'medium'),
(924, 65, 'medium'),
(925, 100, 'good'),
(926, 97, 'good'),
(927, 68, 'medium'),
(928, 92, 'good'),
(929, 85, 'medium'),
(930, 92, 'good'),
(931, 91, 'good'),
(932, 96, 'good'),
(933, 90, 'good'),
(934, 95, 'good'),
(935, 91, 'good'),
(936, 65, 'medium'),
(937, 80, 'medium'),
(938, 97, 'good'),
(939, 79, 'medium'),
(940, 83, 'medium'),
(941, 70, 'medium'),
(942, 86, 'good'),
(943, 75, 'medium'),
(944, 88, 'good'),
(945, 81, 'medium'),
(946, 94, 'good'),
(947, 63, 'medium'),
(948, 65, 'medium'),
(949, 98, 'good'),
(950, 64, 'medium'),
(951, 83, 'medium'),
(952, 69, 'medium'),
(953, 85, 'medium'),
(954, 70, 'medium'),
(955, 81, 'medium'),
(956, 95, 'good'),
(957, 67, 'medium'),
(958, 96, 'good'),
(959, 82, 'medium'),
(960, 63, 'medium'),
(961, 79, 'medium'),
(962, 84, 'medium'),
(963, 86, 'good'),
(964, 76, 'medium'),
(965, 78, 'medium'),
(966, 80, 'medium'),
(967, 75, 'medium'),
(968, 94, 'good'),
(969, 95, 'good'),
(970, 81, 'medium'),
(971, 79, 'medium'),
(972, 93, 'good'),
(973, 70, 'medium'),
(974, 83, 'medium'),
(975, 83, 'medium'),
(976, 93, 'good'),
(977, 78, 'medium'),
(978, 82, 'medium'),
(979, 66, 'medium'),
(980, 78, 'medium'),
(981, 80, 'medium'),
(982, 74, 'medium'),
(983, 95, 'good'),
(984, 90, 'good'),
(985, 61, 'medium'),
(986, 91, 'good'),
(987, 85, 'medium'),
(988, 85, 'medium'),
(989, 88, 'good'),
(990, 98, 'good'),
(991, 72, 'medium'),
(992, 70, 'medium'),
(993, 69, 'medium'),
(994, 61, 'medium'),
(995, 80, 'medium'),
(996, 86, 'good'),
(997, 71, 'medium'),
(998, 68, 'medium'),
(999, 65, 'good'),
(1000, 65, 'good'),
(1003, 86, 'good');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `procesos`
--
ALTER TABLE `procesos`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `procesos`
--
ALTER TABLE `procesos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1004;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
