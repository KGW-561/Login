package com.team3.scvs.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserDTO {

    private Long userId;
    private String email;
    private String password;
    private String nickname;
    private String userrole;
}
