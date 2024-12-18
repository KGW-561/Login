package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CommunityCommentDTO {
    private long communityCommentId;
    private long communityId;
    private long userId;
    private String comment;
    private LocalDateTime publishedAt;
    private LocalDateTime updatedAt;
}
