drop database if exists dbMediclin;

create database dbMediclin;

use dbMediclin;

create table consultorios(
	id int primary key auto_increment,
    nombre varchar(20)
);

create table medicos(
	id int primary key auto_increment,
    RFC varchar(30),
    nombreCompleto varchar(150),
    cedula varchar(30),
    correo varchar(50),
    pass varchar(50),
    rol varchar(20),
    id_consultorio int,
    
    foreign key (id_consultorio) references consultorios(id)
);


create table pacientes(
	id int primary key auto_increment,
    nombreCompleto varchar(150),
    fechaNacimiento date,
    antecedentes text,
    alergias text,
    enfermedades text,
    id_medico int,
    
    foreign key (id_medico) references medicos(id)
);

create table expedientes(
	id int primary key auto_increment,
    codigo varchar(50),
    fechaCreacion datetime,
    id_paciente int,
    
    foreign key (id_paciente) references pacientes(id)
);

create table citas(
	id int primary key auto_increment,
    fecha datetime,
    peso decimal(6,3),
    altura decimal(4,2),
    temperatura decimal(4,2),
    bpm decimal(10,2),
    oxigenacion decimal(10,2),
    glucosa decimal(10,2),
    edad tinyint,
    sintomas text,
    diagnostico text,
    tratamiento text,
    estudios text,
    id_expediente int,
    
    foreign key (id_expediente) references expedientes(id)
);


