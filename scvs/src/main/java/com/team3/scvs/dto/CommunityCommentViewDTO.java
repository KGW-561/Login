package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor // 기본 생성자 생성
@AllArgsConstructor // 모든 필드를 받는 생성자 생성
public class CommunityCommentViewDTO {
    private long id;
    private long userId;
    private long communityId;
    private String nickname;
    private String comment;
    private LocalDateTime publishedAt;
    private LocalDateTime updatedAt;
    private String timeAgo;
}
