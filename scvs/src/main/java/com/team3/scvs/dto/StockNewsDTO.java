package com.team3.scvs.dto;

import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StockNewsDTO {

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
