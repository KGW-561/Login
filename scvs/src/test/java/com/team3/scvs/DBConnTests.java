package com.team3.scvs;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.sql.DataSource;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

@SpringBootTest
public class DBConnTests {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private DataSource dataSource;

    @Test
    void testConnection() {
        try {
            String result = jdbcTemplate.queryForObject("SELECT VERSION()", String.class);
            System.out.println("DB 연결 성공!\nMySQL 버전: " + result);
            String url = dataSource.getConnection().getMetaData().getURL();
            System.out.println("DB 연결 URL: " + url);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("DB 연결 실패!");
        }
    }
}
