package com.team3.scvs.controller;

import com.team3.scvs.dto.PSADTO;
import com.team3.scvs.entity.PSAEntity;
import com.team3.scvs.service.PSAService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;

import java.time.format.DateTimeFormatter;

@Controller
public class PSAController {

    @Autowired
    private PSAService psaService;

    /**
     * 공지사항 목록 조회
     */

    @GetMapping("/PSA-list")
    public String listAllPSAs(
            @RequestParam(defaultValue = "1") int page, // 기본값: 첫 페이지
            @RequestParam(defaultValue = "20") int size, // 기본값: 한 페이지에 20개
            @RequestParam(defaultValue = "") String query, // 검색어 기본값
            Model model) {

        // 공지사항 페이지 데이터 가져오기
        Page<PSADTO> psaPage;
        if (query.isEmpty()) {
            // 검색어가 없는 경우 전체 조회
            psaPage = psaService.findAllPSAsPaginated(page - 1, size);
        } else {
            // 검색어가 있는 경우 제목으로 검색
            psaPage = psaService.searchPSAsByTitlePaginated(query, page - 1, size);
        }

        model.addAttribute("psas", psaPage.getContent()); // 현재 페이지 데이터
        model.addAttribute("currentPage", page); // 사용자에게 보여줄 페이지 번호
        model.addAttribute("totalPages", psaPage.getTotalPages());
        model.addAttribute("query", query); // 검색어 유지

        return "PSA/PSA-list";
    }

    /**
     * 공지사항 상세 조회
     */

    @GetMapping("/PSA-detail/{id}")
    public String viewPSADetail(@PathVariable Long id, Model model) {
        // 데이터베이스에서 공지사항 조회
        PSADTO psaDTO = psaService.findPSAById(id); // <변경됨> DTO로 조회

        if (psaDTO == null) {
            // 해당 ID의 공지사항이 없는 경우 404 페이지로 리다이렉트
            return "redirect:/error/404";
        }

        // 작성일을 문자열로 변환
        String formattedDate = (psaDTO.getPublishedAt() != null)
                ? psaDTO.getPublishedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"))
                : "작성일 정보 없음";

        // 이전 글, 다음 글 호출
        PSADTO previousPSA = psaService.findPreviousPSA(id);
        PSADTO nextPSA = psaService.findNextPSA(id);

        // 모델에 데이터 추가
        model.addAttribute("psa", psaDTO);
        model.addAttribute("publishedAt", formattedDate);
        model.addAttribute("previousPSA", previousPSA);
        model.addAttribute("nextPSA", nextPSA);

        return "PSA/PSA-detail"; // Thymeleaf 템플릿 경로
    }

    /**
     * 공지 추가 화면
     */
    @GetMapping("/PSA-add")
    public String viewPSAAddPage(Model model) {
        // 로그인 상태 기본값 설정 (로그인 관련 로직 없이 기본값만 설정)

        return "PSA/PSA-add"; // Thymeleaf 템플릿 경로
    }

    @PostMapping("/PSA-add")
    public String addPSA(@RequestParam String title, @RequestParam String content, Model model) {
        // 서버 측 검증: 제목과 내용이 비어 있거나 공백만 포함된 경우
        if (title == null || title.trim().isEmpty() || content == null || content.trim().isEmpty()) {
            model.addAttribute("error", "제목과 내용을 올바르게 입력해 주세요.");
            return "PSA/PSA-add"; // 입력 폼으로 다시 이동
        }

        // 데이터 저장 로직
        PSADTO psaDTO = new PSADTO();
        psaDTO.setTitle(title.trim());
        psaDTO.setContent(content.trim());
        psaService.savePSA(psaDTO);

        return "redirect:/PSA-list"; // 저장 후 목록 페이지로 리다이렉트
    }
    /**
     * 공지 수정 화면
     */

    @GetMapping("/PSA/update/{id}")
    public String viewUpdatePSAPage(@PathVariable Long id, Model model) {
        PSADTO psaDTO = psaService.findPSAById(id);
        if (psaDTO == null) {
            return "redirect:/error/404"; // ID에 해당하는 공지가 없으면 404 페이지로 리다이렉트
        }

        model.addAttribute("psa", psaDTO);
        return "PSA/PSA-update"; // 수정 화면 템플릿
    }

    @PostMapping("/PSA/update/{id}")
    public String updatePSA(@PathVariable Long id, @RequestParam String title, @RequestParam String content, Model model) {

        // 공백 검증 로직 추가
        if (title.trim().isEmpty() || content.trim().isEmpty()) {
            model.addAttribute("error", "제목과 내용을 올바르게 입력해 주세요."); // <추가됨>
            PSADTO psadto = psaService.findPSAById(id); // 기존 데이터를 다시 불러오기
            model.addAttribute("psa", psadto); // 기존 데이터 모델에 추가
            return "PSA/PSA-update"; // 수정 화면으로 다시 이동
        }

        psaService.updatePSA(id, title, content); // <변경됨> 서비스 계층에 변경된 DTO 데이터 전달
        return "redirect:/PSA-detail/" + id;
    }

    /**
     * 공지 삭제
     */

    @GetMapping("/PSA/delete/{id}")
    public String deletePSA(@PathVariable Long id) {
        psaService.deletePSAById(id);
        return "redirect:/PSA-list";
    }

    /**
     * 관리자 권한 여부 확인
     */

    private boolean checkIfAdmin() {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        if (principal instanceof UserDetails) {
            UserDetails userDetails = (UserDetails) principal;
            return userDetails.getAuthorities().stream()
                    .anyMatch(auth -> auth.getAuthority().equals("ROLE_ADMIN"));
        }

        return false;
    }
}
