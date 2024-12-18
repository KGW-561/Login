package com.team3.scvs.entity;

import jakarta.persistence.*;
import lombok.*;
import jakarta.persistence.Entity;

import java.time.LocalDateTime;

@Entity
@Table(name = "vw_stock_news")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StockNewsEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String stockNewsId;

    private String title;

    private String source;

    private String imageLink;

    private String content;

    private String sentiment;

    private LocalDateTime publishedAt;

    private String link;

    private long tickerId;

    private String market;
}
