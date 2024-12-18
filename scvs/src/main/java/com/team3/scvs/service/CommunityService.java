package com.team3.scvs.service;

import com.team3.scvs.dto.*;
import com.team3.scvs.entity.*;
import com.team3.scvs.repository.*;
import com.team3.scvs.util.ConvertUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class CommunityService {

    private final CommunityStockInfoRepository communityStockInfoRepository;
    private final CommunityVoteRepository communityVoteRepository;
    private final CommunityRepository communityRepository;
    private final CommunityCommentRepository communityCommentRepository;
    private final UserRepository userRepository;
    private final CommunityCommentViewRepository communityCommentViewRepository;
    private final UserVoteRepository userVoteRepository;
    private final StocksRepository stocksRepository;
    private final StocksNewsTitleRepository stocksNewsRepository;

    //주식 기초 정보
    public CommunityStockInfoDTO getStockInfo(Long tickerId) {
        // 엔티티 조회
        CommunityStockInfoEntity entity = communityStockInfoRepository.findById(tickerId).orElse(null);
        // 엔티티가 존재하지 않으면 null 반환
        if (entity == null) {
            return null;
        }
        // DTO로 변환하여 반환
        return ConvertUtil.convertToDTO(entity);
    }
    // 주식 투표 정보
    public CommunityVoteDTO getVoteInfo(long communityId) {
        // 엔티티 조회
        CommunityVoteEntity voteInfo = communityVoteRepository.findByCommunity_CommunityId(communityId).orElse(null);
        //엔티티가 없으면 새로운 엔티티 생성
        if (voteInfo == null) {
            voteInfo = new CommunityVoteEntity();
            voteInfo.setCommunity(new CommunityEntity());
            voteInfo.getCommunity().setCommunityId(communityId);
            voteInfo.setPositiveVotes(0);
            voteInfo.setNegativeVotes(0);
            voteInfo = communityVoteRepository.save(voteInfo);
        }
        // DTO로 변환하여 반환
        return ConvertUtil.convertToDTO(voteInfo);
    }
    // 주식 투표
    public boolean castVote(UserVoteDTO userVoteDTO, String voteType) {
        // 엔티티 조회
        CommunityVoteEntity voteInfo = communityVoteRepository.findByCommunity_CommunityId(userVoteDTO.getCommunityId())
                .orElseThrow(() -> new IllegalArgumentException("해당 communityId에 대한 투표 데이터가 존재하지 않습니다."));
        // 엔티티 조회
        UserVoteEntity userVote = userVoteRepository.findByUserIdAndCommunityId(userVoteDTO.getUserId(), userVoteDTO.getCommunityId())
                .orElseGet(() -> {
                    //엔티티가 없으면 새로운 엔티티 생성
                    UserVoteEntity newUserVote = new UserVoteEntity();
                    newUserVote.setUserId(userVoteDTO.getUserId());
                    newUserVote.setCommunityId(userVoteDTO.getCommunityId());
                    newUserVote.setVote(false);
                    newUserVote.setCreatedAt(LocalDateTime.now());
                    return userVoteRepository.save(newUserVote);
                });
        //투표했으면 false
        if (userVote.isVote()) {
            return false;
        }
        //투표 정보 반환
        switch (voteType.toLowerCase()) {
            case "positive":
                voteInfo.setPositiveVotes(voteInfo.getPositiveVotes() + 1);
                break;
            case "negative":
                voteInfo.setNegativeVotes(voteInfo.getNegativeVotes() + 1);
                break;
            default:
                throw new IllegalArgumentException("올바르지 않은 투표 유형입니다: " + voteType);
        }
        //엔티티 저장
        userVote.setVote(true);
        userVoteRepository.save(userVote);
        communityVoteRepository.save(voteInfo);

        return true;
    }
    //토론방 정보
    public CommunityDTO getOrCreateCommunity(Long tickerId) {
        // tickerId로 CommunityEntity 조회
        CommunityEntity community = communityRepository.findByTickerId(tickerId).orElse(null);

        if (community == null) {
            // 조회 결과가 없으면 새 엔티티 생성
            CommunityEntity newCommunity = new CommunityEntity();
            newCommunity.setTickerId(tickerId); // tickerId 설정
            community = communityRepository.save(newCommunity); // 저장 후 반환
        }

        // convertToDTO 메서드를 사용하여 CommunityDTO로 변환
        return ConvertUtil.convertToDTO(community);
    }
    //토론방에 댓글 정보
    public List<CommunityCommentViewDTO> getComments(Long communityId) {
        return communityCommentViewRepository.findAllByCommunityIdOrderByPublishedAtDesc(communityId)
                .stream()
                .map(ConvertUtil::convertToDTO)
                .collect(Collectors.toList());
    }
    // 댓글 추가
    public void addComment(CommunityCommentDTO commentDTO) {
        // CommunityEntity 조회
        CommunityEntity community = communityRepository.findById(commentDTO.getCommunityId())
                .orElseThrow(() -> new IllegalArgumentException("해당 communityId에 대한 커뮤니티가 존재하지 않습니다."));

        // UserEntity 조회
        UserEntity user = userRepository.findById(commentDTO.getUserId())
                .orElseThrow(() -> new IllegalArgumentException("해당 userId에 대한 사용자가 존재하지 않습니다."));

        // 새로운 댓글 엔티티 생성 및 설정
        CommunityCommentEntity newComment = new CommunityCommentEntity();
        newComment.setCommunity(community);
        newComment.setUser(user);
        newComment.setComment(commentDTO.getComment());

        // 댓글 저장
        communityCommentRepository.save(newComment);
    }
    //댓글 삭제
    public boolean deleteComment(Long communityCommentId, Long userId) {
        // 댓글 조회
        CommunityCommentEntity comment = communityCommentRepository.findById(communityCommentId)
                .orElseThrow(() -> new IllegalArgumentException("해당 댓글이 존재하지 않습니다."));
        // 댓글 삭제
        communityCommentRepository.delete(comment);
        return true; // 성공적으로 삭제되었음을 반환
    }
    //댓글 수정
    public boolean editComment(Long commentId, Long userId, String updatedComment) {
        // 댓글 조회
        CommunityCommentEntity comment = communityCommentRepository.findById(commentId)
                .orElseThrow(() -> new IllegalArgumentException("해당 댓글이 존재하지 않습니다."));

        // 댓글 작성자와 로그인 사용자 일치 여부 확인
        if (!comment.getUser().getUserId().equals(userId)) {
            throw new SecurityException("본인이 작성한 댓글만 수정할 수 있습니다.");
        }

        // 댓글 내용 업데이트
        comment.setComment(updatedComment);
        comment.setUpdatedAt(LocalDateTime.now()); // 수정 시간 갱신
        communityCommentRepository.save(comment);

        return true; // 성공적으로 수정되었음을 반환
    }
    // 주식에 다양한 정보
    public Optional<StocksDTO> getStocksInfo(Long tickerId) {
        return stocksRepository.findByTickerId(tickerId).map(ConvertUtil::convertToDTO);
    }

    //주식 관련 뉴스
    public List<StockNewsTitleDTO> getStocksNewsTitle(Long tickerId) {
        return stocksNewsRepository.findLatestByTickerId(tickerId).stream()
                .map(ConvertUtil::convertToDTO)
                .limit(3)
                .collect(Collectors.toList());
    }


}
