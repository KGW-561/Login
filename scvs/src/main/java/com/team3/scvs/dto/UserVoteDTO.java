package com.team3.scvs.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserVoteDTO {

    private long uservoteId;       // UserVote ID
    private long userId;           // User ID
    private long communityId;      // Community ID
    private boolean vote;          // 투표 상태 (true/false)
    private LocalDateTime createdAt; // 투표 생성 시간
}
