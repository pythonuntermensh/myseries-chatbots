package com.myapps.parsermyseries;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ParserMySeriesApplication {

    public static void main(String[] args) {
        SpringApplication.run(ParserMySeriesApplication.class, args);
    }

}
