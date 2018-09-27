/*
All auth tables
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `url_route` text DEFAULT NULL COMMENT 'url集合',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户组表';

-- ----------------------------
-- Table structure for auth_url
-- ----------------------------
DROP TABLE IF EXISTS `auth_url`;
CREATE TABLE `auth_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT 'url描述名称',
  `url` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限路由表';

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `super` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否为管理员[(0,普通用户),(1, 管理员)]',
  `lock` tinyint(4) NOT NULL DEFAULT 0 COMMENT '账户是否锁定[(0, 锁定),(1,未锁定)]',
  `group_id` int(11) NOT NULL,
  `ctime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '账户创建时间',
  `ltime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '账户锁定时间',
  PRIMARY KEY (`id`),
  KEY `group` (`group_id`),
  CONSTRAINT `group` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';
SET FOREIGN_KEY_CHECKS=1;
