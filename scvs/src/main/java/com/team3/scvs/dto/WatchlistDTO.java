package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WatchlistDTO {
    private Long userWatchlistId; // 관심 목록 ID
    private Long userId;          // 사용자 ID
}
