package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "kor_econ_news")
@Getter
@Setter
public class KorEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long korEconNewsId;

    private String title;
    private String source;
    private String imageLink;
    private String content;
    private LocalDateTime publishedAt;
    private String link;

}
