drop database if exists dbMediclin;

create database dbMediclin;

use dbMediclin;

create table consultorios(
	id int primary key auto_increment,
    nombre varchar(20) not null
);

create table medicos(
	id int primary key auto_increment,
    RFC varchar(30) not null,
    nombreCompleto varchar(150) not null,
    cedula varchar(30) not null,
    correo varchar(50) not null,
    hashP varchar(255) not null,
    rol varchar(20) not null,
    id_consultorio int not null,
    
    foreign key (id_consultorio) references consultorios(id)
);


create table pacientes(
	id int primary key auto_increment,
    nombreCompleto varchar(150) not null,
    fechaNacimiento date not null,
    antecedentes text,
    alergias text,
    enfermedades text,
    fechaCreacion datetime not null,
    id_medico int not null,
    
    foreign key (id_medico) references medicos(id) on delete cascade
);

create table expedientes(
	id int primary key auto_increment,
    codigo varchar(50) not null,
    fechaCreacion datetime not null,
    id_paciente int not null,
    
    foreign key (id_paciente) references pacientes(id) on delete cascade
);


create table citas(
	id int primary key auto_increment,
    fecha date not null,
    hora time not null,
    peso decimal(6,3) not null,
    altura decimal(4,2) not null,
    temperatura decimal(4,2) not null,
    bpm decimal(10,2) not null,
    oxigenacion decimal(10,2) not null,
    glucosa decimal(10,2) not null,
    edad tinyint not null,
    sintomas text not null,
    diagnostico text not null,
    tratamiento text not null,
    estudios text not null,
    id_consultorio int not null,
    id_paciente int not null,
    nombrePDF text not null,
    estado tinyint not null,
    
    foreign key (id_paciente) references pacientes(id) on delete cascade,
    foreign key (id_consultorio) references consultorios(id)
);

insert into consultorios(nombre)
values
('A1'),
('A2'),
('B1'),
('B2'),
('C1'),
('C2');

insert into medicos(RFC,nombreCompleto,cedula,correo,hashP,rol,id_consultorio)
values
('admin','admin','admin','admin@gmail.com','$2b$12$8Yzw7cai8s2naahZINBJUefCpwVguOdOQE2NXVPKQSJ1.ypLnosde','1',1);
