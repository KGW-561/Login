package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor  // 기본 생성자
@AllArgsConstructor // 모든 필드를 받는 생성자
public class StockNewsTitleDTO {

    private String id; // stocker_news_id

    private String title;

    private long tickerId; // ticker_id

    private String sentiment;

    private LocalDateTime publishedAt;

    private String market;
}
