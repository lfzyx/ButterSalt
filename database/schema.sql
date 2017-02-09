drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  role_id integer not null
);

drop table if exists user_role;
create table user_role (
  id integer primary key autoincrement,
  role_name text not null,
  salt_api_username text not null,
  salt_api_password text not null
);

drop table if exists role_authority;
create table role_authority (
  id integer primary key autoincrement,
  authority_name text not null,
  role_id integer not null
);

drop table if exists moudle_execute_history;
create table moudle_execute_history (
  id integer primary key autoincrement,
  tgt text not null,
  fun text not null,
  args text,
  kwargs text,
  user_id integer not null
);