from datetime import datetime

from sqlalchemy import (DECIMAL, TIMESTAMP, CheckConstraint, Column, DateTime,
                        ForeignKey, Integer, PrimaryKeyConstraint, String,
                        Text, UniqueConstraint)
from sqlalchemy.orm import relationship

from src.infra.models.base import (Base, BaseEntity, NamedEntity,
                                   NamedEntityWithDescription,
                                   NamedEntityWithShortName,
                                   SoftDeletableEntity)


class Country(NamedEntity):
    """
    Страна
    """

    __tablename__ = "countries"


class LocationType(NamedEntityWithShortName):
    """
    Тип населенного пункта
    """

    __tablename__ = "location_types"
    __name_length__ = 50


class Location(NamedEntity):
    """
    Населенный пункт
    """

    __tablename__ = "locations"

    country_id = Column(
        Integer, ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False
    )
    location_type_id = Column(
        Integer, ForeignKey("location_types.id", ondelete="RESTRICT"), nullable=False
    )

    country = relationship("Country")
    location_type = relationship("LocationType")

    __table_args__ = UniqueConstraint("name", "country_id", name="uq_location_country")


class Address(SoftDeletableEntity):
    """
    Адрес
    """

    __tablename__ = "addresses"

    street_address = Column(String(250), nullable=False)
    postal_code = Column(String(20))

    location_id = Column(
        Integer, ForeignKey("locations.id", ondelete="RESTRICT"), nullable=False
    )

    location = relationship("Location")


class Hotel(NamedEntity):
    """
    Отель
    """

    __tablename__ = "hotels"
    __name_length__ = 250

    star_rating = Column(Integer, nullable=False)

    address_id = Column(
        Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), nullable=False
    )

    address = relationship("Address")

    __table_args__ = (
        CheckConstraint(
            "star_rating >= 1 AND star_rating <= 5", name="chk_star_rating"
        ),
    )


class RoomType(NamedEntityWithDescription):
    """
    Тип комнаты
    """

    __tablename__ = "room_types"
    __name_length__ = 50


class Amenity(NamedEntityWithDescription):
    """
    Удобство (например, Wi-Fi)
    """

    __tablename__ = "amenities"


class Room(SoftDeletableEntity):
    """
    Комната
    """

    __tablename__ = "rooms"

    room_number = Column(String(10), nullable=False)
    price_per_night = Column(DECIMAL, nullable=False)
    capacity = Column(Integer, nullable=False)

    hotel_id = Column(
        Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False
    )
    room_type_id = Column(
        Integer, ForeignKey("room_types.id", ondelete="RESTRICT"), nullable=False
    )

    hotel = relationship("Hotel")
    room_type = relationship("RoomType")

    __table_args__ = UniqueConstraint(
        "hotel_id", "room_number", name="uq_hotel_id_room_number"
    )


class RoomAmenity(Base):
    """
    Удобство комнаты
    """

    __tablename__ = "room_amenities"

    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    amenity_id = Column(
        Integer, ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("room_id", "amenity_id", name="pk_room_amenities"),
    )


class User(SoftDeletableEntity):
    """
    Пользователь
    """

    __tablename__ = "users"

    email = Column(String(250), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20))
    hashed_password = Column(Text)


class BookingStatus(NamedEntity):
    """
    Статус бронирования
    """

    __tablename__ = "booking_statuses"
    __name_length__ = 50


class Booking(SoftDeletableEntity):
    """
    Бронирование
    """

    __tablename__ = "bookings"

    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_price = Column(DECIMAL, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="RESTRICT"))
    booking_status_id = Column(
        Integer, ForeignKey("booking_statuses.id", ondelete="SET NULL")
    )

    user = relationship("User")
    room = relationship("Room")
    booking_status = relationship("BookingStatus")

    __table_args__ = (
        CheckConstraint("check_in_date < check_out_date", name="chk_valid_dates"),
    )


class Review(SoftDeletableEntity):
    """
    Отзыв
    """

    __tablename__ = "reviews"

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    hotel_id = Column(
        Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User")
    hotel = relationship("Hotel")

    __table_args__ = CheckConstraint("rating >= 1 AND rating <= 5", "chk_rating")


class SearchHistory(BaseEntity):
    """
    История поиска
    """

    __tablename__ = "search_history"

    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    adults = Column(Integer)
    children = Column(Integer)
    search_timestamp = Column(TIMESTAMP, default=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"))

    user = relationship("User")
    location = relationship("Location")
