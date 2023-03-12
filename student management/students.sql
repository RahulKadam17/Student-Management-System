-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 11, 2023 at 02:14 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `students`
--

-- --------------------------------------------------------

CREATE TABLE `trig` (
  `tid` int(11) NOT NULL,
  `rollno` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trig`
--





CREATE TABLE `department` (
  `cid` varchar(50) NOT NULL,
  `branch` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `department`
  ADD PRIMARY KEY (`cid`);

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`cid`, `branch`) VALUES
('ISE', 'Information Science'),
('EC', 'Electronic and Communication'),
('EEE', 'Electrical & Electronic'),
('CV', 'Civil'),
('CSE', 'Computer Science'),
('BT', 'Biotechnology'),
('ME', 'Mechanical'),
('ET', 'Electronics and Telecommunication'),
('CH', 'Chemical'),
('IEM', 'Industrial Engineering and Management'),
('EI', 'Electronic and Instrumentation');

-- --------------------------------------------------------


CREATE TABLE `course` (
  `coursecode` varchar(10) NOT NULL,
   `coursename` varchar(50) NOT NULL,
  `branch_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
  
  
  ALTER TABLE `course`
  ADD PRIMARY KEY (`coursecode`);


ALTER TABLE `course` ADD CONSTRAINT `c1` FOREIGN KEY (`branch_id`) REFERENCES `department`(`cid`) ON DELETE CASCADE ON UPDATE RESTRICT;

INSERT INTO `course` ( `coursecode`, `coursename`,`branch_id`) VALUES
('18CS52', 'FAFL','CSE'),
('18CS53', 'DBMS','CSE'),
('18CS54', 'NPS','CSE'),
('18IS55', 'SE','ISE'),
('18G5B09', 'OR','IEM');


-- --------------------------------------------------------

CREATE TABLE `staff` (
  `staffid` varchar(50) NOT NULL ,
   `email` varchar(50) NOT NULL , 
   `name` varchar(50) NOT NULL ,
    `phone` varchar(50) NOT NULL , 
    `specialization` varchar(50) NOT NULL , 
    PRIMARY KEY (`staffid`)
    ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `staff` ( `staffid`, `email`,`name`,`phone`,`specialization`) VALUES
('1', 'abc@rvce.edu.in','xyz','99999991','A'),
('2', 'xxy@rvce.edu.in','abc','998899991','B'),
('3', 'bhy@rvce.edu.in','ayuy','998892991','C'),
('4', 'bpj@rvce.edu.in','ay','998799991','D'),
('10', 'jkl@rvce.edu.in','abcd','998666991','E');


-- --------------------------------------------------------
CREATE TABLE `teach` (
  `tid` INT NOT NULL AUTO_INCREMENT ,
   `course` varchar(50) NOT NULL , 
   `staffid` varchar(50) NOT NULL , 
   PRIMARY KEY (`tid`)) 
   ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 ;
    
   ALTER TABLE `teach` ADD CONSTRAINT `t1` FOREIGN KEY (`course`) REFERENCES `course`(`coursecode`) ON DELETE CASCADE ON UPDATE RESTRICT;
   ALTER TABLE `teach` ADD CONSTRAINT `t2` FOREIGN KEY (`staffid`) REFERENCES `staff`(`staffid`) ON DELETE CASCADE ON UPDATE RESTRICT;
      
  INSERT INTO `teach` (`course`,`staffid`) VALUES
  ('18CS52', '1'),
  ('18CS53', '2'),
  ('18CS54', '3'),
  ('18IS55', '4'),
  ('18G5B09', '10');

-- --------------------------------------------------------


CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `rollno` varchar(20) NOT NULL,
  `sname` varchar(50) NOT NULL,
  `sem` int(20) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` varchar(12) NOT NULL,
  `address` text NOT NULL,
  `counsellor` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



ALTER TABLE `student` ADD CONSTRAINT `s1` FOREIGN KEY (`branch`) REFERENCES `department`(`cid`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `student` ADD CONSTRAINT `s2` FOREIGN KEY (`counsellor`) REFERENCES `staff`(`staffid`) ON DELETE CASCADE ON UPDATE RESTRICT;
--ALTER TABLE `student`
 -- MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
--
-- Triggers `student`
--
DELIMITER $$
CREATE TRIGGER `DELETE` BEFORE DELETE ON `student` FOR EACH ROW INSERT INTO trig VALUES(null,OLD.rollno,'STUDENT DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Insert` AFTER INSERT ON `student` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.rollno,'STUDENT INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `UPDATE` AFTER UPDATE ON `student` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.rollno,'STUDENT UPDATED',NOW())
$$
DELIMITER ;
ALTER TABLE `student`
  ADD PRIMARY KEY (`rollno`);
-- --------------------------------------------------------



CREATE TABLE `enrol`(
  `eid` int(11) NOT NULL,
  `rollno` varchar(10) NOT NULL,
  `coursecode` varchar(10) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `enrol`
 ADD PRIMARY KEY(`eid`);

 ALTER TABLE `enrol`
  MODIFY `eid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

  ALTER TABLE `enrol` ADD CONSTRAINT `e1` FOREIGN KEY (`coursecode`) REFERENCES `course`(`coursecode`) ON DELETE CASCADE ON UPDATE RESTRICT;
  ALTER TABLE `enrol` ADD CONSTRAINT `e2` FOREIGN KEY (`rollno`) REFERENCES `student`(`rollno`) ON DELETE CASCADE ON UPDATE RESTRICT;

--  INSERT INTO `enrol` ( `eid`,`rollno`,`coursecode`) VALUES
--  (1,'1rv20cs130','18cs42');



-- --------------------------------------------------------
--
-- Table structure for table `attendence`
--

CREATE TABLE `attendence` (
  `aid` int(11) NOT NULL,
  `rollno` varchar(20) NOT NULL,
  `course` varchar(20) NOT NULL,
  `attendance` int(100) NOT NULL
   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `attendence`
  ADD PRIMARY KEY (`aid`);

ALTER TABLE `attendence`
  MODIFY `aid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

  
ALTER TABLE `attendence` ADD CONSTRAINT `at1` FOREIGN KEY (`course`) REFERENCES `course`(`coursecode`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `attendence` ADD CONSTRAINT `at2` FOREIGN KEY (`rollno`) REFERENCES `student`(`rollno`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Dumping data for table `attendence`
--


-- INSERT INTO `attendence` (`aid`, `rollno`, `attendance`) VALUES
-- (6, '1ve17cs012', 98);

-- --------------------------------------------------------



-- Table structure for table `grade`
--
CREATE TABLE `grade`(
  `gid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `rollno` varchar(10) NOT NULL,
  `coursecode` varchar(10) NOT NULL,
   `marks` int(11) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `grade`
 ADD PRIMARY KEY(`gid`);

ALTER TABLE `grade`
  MODIFY `gid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `grade` ADD CONSTRAINT `g1` FOREIGN KEY (`rollno`) REFERENCES `student`(`rollno`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `grade` ADD CONSTRAINT `g2` FOREIGN KEY (`coursecode`) REFERENCES `course`(`coursecode`) ON DELETE CASCADE ON UPDATE RESTRICT;



-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Indexes for table `trig`
--
ALTER TABLE `trig`
  ADD PRIMARY KEY (`tid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

-- ALTER TABLE `enrol`
--   ADD CONSTRAINT `usn` FOREIGN KEY (`usn`) REFERENCES `student`(`rollno`) ON DELETE RESTRICT ON UPDATE RESTRICT;
--
-- AUTO_INCREMENT for dumped tables
--


 
--
-- AUTO_INCREMENT for table `attendence`
--

-- SELECT name FROM `staff` WHERE staffid IN( SELECT staffid FROM `teach` s WHERE s.course IN (SELECT sb.coursecode FROM `enrol` sb));

ALTER TABLE `trig`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
