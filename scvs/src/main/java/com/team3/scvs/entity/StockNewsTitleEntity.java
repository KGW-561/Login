package com.team3.scvs.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.Immutable;

import java.time.LocalDateTime;

@Entity
@Data
@Immutable //읽기전용 Entity
@NoArgsConstructor  // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
@Table(name = "vw_stock_title_news")
public class StockNewsTitleEntity {

    @Id
    @Column(name = "stocker_news_id")
    private String Id;

    private String title;

    @Column(name = "ticker_id")
    private long tickerId;

    private String sentiment;

    @Column(name = "published_at")
    private LocalDateTime publishedAt;

    private String market;
}
