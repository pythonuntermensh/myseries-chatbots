package com.myapps.seriesmanager.repository;

import com.myapps.seriesmanager.entity.SeriesEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SeriesRepository extends JpaRepository<SeriesEntity, Long> {
    SeriesEntity findByName(String name);
    SeriesEntity findByNameAndAdditional(String name, String additional);
    List<SeriesEntity> findAllByName(String name);
    List<SeriesEntity> findAllByLowRegisterName(String name);
    List<SeriesEntity> findAllByLowRegisterNameAndAdditional(String name, String additional);
}
