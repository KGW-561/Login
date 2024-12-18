package com.team3.scvs.controller;

import com.team3.scvs.dto.UserDTO;
import com.team3.scvs.service.AdminUserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;



@Slf4j
@Controller
@RequestMapping("/admin")
public class AdminController {

    private final AdminUserService adminUserService;
    // 생성자 주입
    public AdminController(AdminUserService adminUserService) {
        this.adminUserService = adminUserService;
    }

    // 유저리스트 전체 불러오기
    @GetMapping("/userList")
    public String getUserListPage(
            @RequestParam(value = "filterDropdown", defaultValue = "email") String filter,
            @RequestParam(value = "findInput", defaultValue = "") String input,
            @RequestParam(value = "page", defaultValue = "0") int page, // 현재 페이지 번호
            @RequestParam(value = "size", defaultValue = "15") int size, // 페이지 크기
            @RequestParam(value = "sortBy", defaultValue = "userId") String sortBy, // 정렬 기준
            @RequestParam(value = "direction", defaultValue = "DESC") String direction, // 정렬 방향
            Model model
    ){
        // 정렬 방향 설정
        Sort sort = direction.equalsIgnoreCase(Sort.Direction.ASC.name())
                ? Sort.by(sortBy).ascending()
                : Sort.by(sortBy).descending();

        // Pageable 객체 생성
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<UserDTO> users = adminUserService.getFilteredUsers(filter, input, pageable); // 필터, 검색, 페이징을 통한 검색

        // 처음, 끝페이징
        int startPage = users.getNumber() > (Math.max(users.getTotalPages() - 3, 0)) ? users.getTotalPages() - 5 : Math.max(0, users.getNumber() - 2);
        int endPage = users.getNumber() < 2 ? (Math.min(users.getTotalPages() - 1, 4)) : Math.min(users.getTotalPages() - 1, users.getNumber() + 2);

        // 모델에 결과 담기
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);

        model.addAttribute("sortBy", sortBy);
        model.addAttribute("direction", direction);
        model.addAttribute("users", users);
        return  "Admin/userList";
    }


    // 유저리스트 검색해서 불러오기
    @PostMapping("/userList")
    public String getUserList(
            @RequestParam("filterDropdown") String filter, // 검색 필터
            @RequestParam("findInput") String input,       // 검색 입력값
            @RequestParam(value = "page", defaultValue = "0") int page, // 현재 페이지 번호
            @RequestParam(value = "size", defaultValue = "15") int size, // 페이지 크기
            @RequestParam(value = "sortBy", defaultValue = "userId") String sortBy, // 정렬 기준
            @RequestParam(value = "direction", defaultValue = "DESC") String direction, // 정렬 방향
            Model model
    ) {
        // 정렬 방향 설정
        Sort sort = direction.equalsIgnoreCase(Sort.Direction.ASC.name())
                ? Sort.by(sortBy).ascending()
                : Sort.by(sortBy).descending();
        // Pageable 객체 생성
        Pageable pageable = PageRequest.of(page, size, sort);

        int startPage;
        int endPage;
        Page<UserDTO> users = adminUserService.getFilteredUsers(filter, input, pageable); // 필터, 검색, 페이징을 통한 검색
        if( users.isEmpty()){
            // 처음, 끝페이징
            startPage = 0;
            endPage = 0;
        }else {
            // 처음, 끝페이징
            startPage = users.getNumber() > (Math.max(users.getTotalPages() - 3, 0)) ? users.getTotalPages() - 5 : Math.max(0, users.getNumber() - 2);
            endPage = users.getNumber() < 2 ? (Math.min(users.getTotalPages() - 1, 4)) : Math.min(users.getTotalPages() - 1, users.getNumber() + 2);
        }
        // 모델에 결과 담기
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);

        model.addAttribute("users", users);
        model.addAttribute("filterDropdown", filter);
        model.addAttribute("findInput", input);
        model.addAttribute("page", page);
        model.addAttribute("size", size);
        model.addAttribute("sortBy", sortBy);
        model.addAttribute("direction", direction);

        // 결과를 보여줄 뷰로 이동
        return "Admin/userList"; // Thymeleaf 템플릿 경로
    }

    // 체크한 유저 삭제
    @PostMapping("/deleteUserList")
    public String deleteUserList(
            @RequestParam(name = "userIds", required = false) List<Long> userIds,
            @RequestParam("filterDropdown") String filter, // 검색 필터
            @RequestParam("findInput") String input,       // 검색 입력값
            @RequestParam(value = "page", defaultValue = "0") int page, // 현재 페이지 번호
            @RequestParam(value = "size", defaultValue = "15") int size, // 페이지 크기
            @RequestParam(value = "sortBy", defaultValue = "userId") String sortBy, // 정렬 기준
            @RequestParam(value = "direction", defaultValue = "DESC") String direction, // 정렬 방향
            Model model
    ){
        // 정렬 방향 설정
        Sort sort = direction.equalsIgnoreCase(Sort.Direction.ASC.name())
                ? Sort.by(sortBy).ascending()
                : Sort.by(sortBy).descending();
        // Pageable 객체 생성
        Pageable pageable = PageRequest.of(page, size, sort);
        // user삭제
        adminUserService.deleteUsers(userIds);

        Page<UserDTO> users = adminUserService.getFilteredUsers(filter, input, pageable); // 필터, 검색, 페이징을 통한 검색

        // 처음, 끝페이징
        int startPage = users.getNumber() > (Math.max(users.getTotalPages() - 3, 0)) ? users.getTotalPages() - 5 : Math.max(0, users.getNumber() - 2);
        int endPage = users.getNumber() < 2 ? (Math.min(users.getTotalPages() - 1, 4)) : Math.min(users.getTotalPages() - 1, users.getNumber() + 2);
        // 모델에 결과 담기
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);

        model.addAttribute("users", users);
        model.addAttribute("filterDropdown", filter);
        model.addAttribute("findInput", input);
        model.addAttribute("page", page);
        model.addAttribute("size", size);
        model.addAttribute("sortBy", sortBy);
        model.addAttribute("direction", direction);
        return "Admin/userList";
    }



}
