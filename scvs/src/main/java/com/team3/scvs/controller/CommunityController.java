package com.team3.scvs.controller;


import com.team3.scvs.dto.*;
import com.team3.scvs.service.CommunityService;
import com.team3.scvs.service.CustomUserDetailsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import org.springframework.ui.Model;

import java.util.List;
import java.util.Optional;


@Controller
public class CommunityController {

    @Autowired
    private CommunityService communityService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    @GetMapping("/community")
    public String community(@RequestParam("tickerId") Long tickerId,
                            Model model) {

        // userId 가져오기
        Long userId = customUserDetailsService.getLoggedInUserId();

        //userRole 가져오기
        String userRole = customUserDetailsService.getLoggedInUserRole();

        // 주식 정보 가져오기
        CommunityStockInfoDTO stockInfo = communityService.getStockInfo(tickerId);

        // 커뮤니티 테이블 가져오기
        CommunityDTO community = communityService.getOrCreateCommunity(tickerId);

        // 투표 결과 가져오기
        Long communityId = community.getCommunityId();
        CommunityVoteDTO voteInfo = communityService.getVoteInfo(communityId);

        // 토론방 코멘트 가져오기
        List<CommunityCommentViewDTO> commentList = communityService.getComments(communityId);

        // 마켓 정보 가져오기
        Optional<StocksDTO> stockinfoOptional = communityService.getStocksInfo(tickerId);
        StocksDTO stocksinfo = stockinfoOptional.orElse(null);

        // 뉴스 제목 가져오기
        List<StockNewsTitleDTO> stocknewsinfo = communityService.getStocksNewsTitle(tickerId);

        // 모델에 데이터 추가
        model.addAttribute("userId", userId);
        model.addAttribute("userRole",userRole);
        model.addAttribute("stockInfo", stockInfo);
        model.addAttribute("voteInfo", voteInfo);
        model.addAttribute("commentList", commentList);
        model.addAttribute("communityId", communityId);
        model.addAttribute("stocksinfo", stocksinfo);
        model.addAttribute("stocknewsinfo", stocknewsinfo);
        return "Stockwatch/community";
    }

    @PostMapping("/addComment")
    public String addComment(@RequestParam("communityId") Long communityId,
                             @RequestParam("tickerId") Long tickerId,
                             @RequestParam("commentInput") String commentInput) {

        Long userId = customUserDetailsService.getLoggedInUserId();

        // 댓글 DTO 생성
        CommunityCommentDTO commentDTO = new CommunityCommentDTO();
        commentDTO.setCommunityId(communityId);
        commentDTO.setUserId(userId);
        commentDTO.setComment(commentInput);

        // 댓글 등록 로직 호출
        communityService.addComment(commentDTO);

        // 등록 후 기존 페이지로 리다이렉트
        return "redirect:/community?tickerId=" + tickerId;
    }

    @PostMapping("/castVote")
    public String castVote(@RequestParam("communityId") Long communityId,
                           @RequestParam("voteType") String voteType,
                           @RequestParam("tickerId") Long tickerId,
                           Model model) {

        Long userId = customUserDetailsService.getLoggedInUserId();
        try {
            // 투표 DTO 생성
            UserVoteDTO userVoteDTO = new UserVoteDTO();
            userVoteDTO.setCommunityId(communityId);
            userVoteDTO.setUserId(userId);

            // 투표 처리 로직 호출
            boolean isVoteSuccessful = communityService.castVote(userVoteDTO, voteType);

            if (!isVoteSuccessful) {
                // 이미 투표한 경우 오류 메시지 추가
                model.addAttribute("voteError", "이미 투표하셨습니다.");
            }
        } catch (IllegalArgumentException e) {
            // 잘못된 입력 처리
            model.addAttribute("voteError", e.getMessage());
        }

        // 기존 페이지로 리다이렉트
        return "redirect:/community?tickerId=" + tickerId;
    }

    @PostMapping("/deleteComment")
    public String deleteComment(@RequestParam("communityCommentId") Long communityCommentId,
                                @RequestParam("tickerId") Long tickerId,
                                Model model) {

        Long userId = customUserDetailsService.getLoggedInUserId();
        try {
            // 삭제 로직 호출
            communityService.deleteComment(communityCommentId, userId);
        } catch (SecurityException e) {
            model.addAttribute("deleteError", e.getMessage());
        } catch (IllegalArgumentException e) {
            model.addAttribute("deleteError", "댓글을 찾을 수 없습니다.");
        }

        // 삭제 후 기존 페이지로 리다이렉트
        return "redirect:/community?tickerId=" + tickerId;
    }

    @PostMapping("/editComment")
    public String editComment(@RequestParam("communityCommentId") Long commentId,
                              @RequestParam("tickerId") Long tickerId,
                              @RequestParam("editedComment") String updatedComment,
                              Model model) {

        Long userId = customUserDetailsService.getLoggedInUserId();

        try {
            // 수정 로직 호출
            communityService.editComment(commentId, userId, updatedComment);
        } catch (SecurityException e) {
            model.addAttribute("editError", e.getMessage());
        } catch (IllegalArgumentException e) {
            model.addAttribute("editError", "댓글을 찾을 수 없습니다.");
        }

        // 수정 후 기존 페이지로 리다이렉트
        return "redirect:/community?tickerId=" + tickerId;
    }
}
