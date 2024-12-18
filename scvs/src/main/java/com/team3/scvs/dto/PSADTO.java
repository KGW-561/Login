package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class PSADTO {
    private Long id;                // 공지사항 ID
    private String title;           // 공지사항 제목
    private String content;         // 공지사항 내용
    private LocalDateTime publishedAt; // 작성 시간
}
