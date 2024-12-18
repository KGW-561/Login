package com.team3.scvs.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CommunityVoteDTO {
    private long communityVoteId;
    private long communityId;
    private long positiveVotes;
    private long negativeVotes;
}
